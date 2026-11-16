from pathlib import Path
import json, shutil, subprocess
import cv2
import numpy as np
import imageio_ffmpeg

out = Path('/Users/g.martins/Downloads/O feed/output/santos-video-test')
source = '/Users/g.martins/Downloads/jersey.mp4'
key_source = Path('/Users/g.martins/.codex/generated_images/01a1ade4-9505-7401-8d70-734d30514dec/exec-0c338c8d-6133-4a6c-b03d-49bdc8c4f158.png')
key_path = out/'santos-video-keyframe.png'
shutil.copy2(key_source, key_path)
frames = np.load(out/'continuous-original-frames.npy')
ref_index = len(frames)//2
ref = frames[ref_index]
h,w = ref.shape[:2]
key = cv2.resize(cv2.imread(str(key_path)), (w,h), interpolation=cv2.INTER_AREA)
# A compact feather outside both silhouettes prevents old sleeve/hem edges leaking.
outline = np.array([(139,111),(125,123),(91,137),(61,157),(37,189),(0,270),(0,295),(43,329),(53,319),(56,345),(58,549),(109,559),(169,566),(231,565),(294,558),(301,329),(307,325),(359,301),(359,269),(329,187),(293,157),(251,134),(216,111)],np.int32)
mask = np.zeros((h,w),np.uint8)
cv2.fillPoly(mask,[outline],255)
mask = cv2.GaussianBlur(mask.astype(np.float32)/255,(0,0),1.5)
# Keep the real wooden hanger wherever it overlaps the replacement collar.
hsv = cv2.cvtColor(ref,cv2.COLOR_BGR2HSV)
hanger = ((hsv[:,:,0]>5)&(hsv[:,:,0]<40)&(hsv[:,:,1]>40)&(hsv[:,:,2]>65)).astype(np.float32)
hanger[:55]=0; hanger[138:]=0
hanger = cv2.GaussianBlur(hanger,(0,0),.6)
mask *= 1-hanger
cv2.imwrite(str(out/'compositing-mask.png'),(mask*255).astype(np.uint8))
gray_ref = cv2.cvtColor(ref,cv2.COLOR_BGR2GRAY)
yy,xx = np.mgrid[:h,:w].astype(np.float32)
grid = np.dstack((xx,yy))
sift=cv2.SIFT_create(nfeatures=1800)
kp_ref,desc_ref=sift.detectAndCompute(gray_ref,None)
matcher=cv2.BFMatcher()
flow_engine=cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
flow_engine.setUseSpatialPropagation(True)
flow_engine.setGradientDescentIterations(25)
flow_engine.setVariationalRefinementIterations(5)
ref_luma=cv2.GaussianBlur(gray_ref.astype(np.float32)+12,(0,0),5)
results=[]
checks=[]
for i,frame in enumerate(frames):
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    if i==ref_index:
        flow=np.zeros((h,w,2),np.float32)
        inliers=0
    else:
        kp,desc=sift.detectAndCompute(gray,None)
        pairs=matcher.knnMatch(desc,desc_ref,k=2)
        good=[a for a,b in pairs if a.distance<.73*b.distance]
        a=np.float32([kp[m.queryIdx].pt for m in good]).reshape(-1,1,2)
        b=np.float32([kp_ref[m.trainIdx].pt for m in good]).reshape(-1,1,2)
        H,inlier_mask=cv2.findHomography(a,b,cv2.RANSAC,2.0)
        inliers=int(inlier_mask.sum())
        init=cv2.perspectiveTransform(grid.reshape(-1,1,2),H).reshape(h,w,2)-grid
        flow=flow_engine.calc(gray,gray_ref,np.ascontiguousarray(init,dtype=np.float32))
    coords=grid+flow
    def warp(img):
        return cv2.remap(img,coords[:,:,0],coords[:,:,1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT_101)
    alpha=warp(mask)[:,:,None]
    replacement=warp(key).astype(np.float32)
    # Transfer only slow real exposure/light variation, not the original print.
    ratio=cv2.GaussianBlur(gray.astype(np.float32)+12,(0,0),5)/np.maximum(warp(ref_luma),12)
    ratio=cv2.GaussianBlur(ratio,(0,0),7)
    ratio=np.clip(ratio,.9,1.1)
    replacement*=ratio[:,:,None]
    composed=np.clip(frame.astype(np.float32)*(1-alpha)+replacement*alpha,0,255).astype(np.uint8)
    results.append(composed)
    if i in [0,ref_index,len(frames)-1]:
        cv2.imwrite(str(out/f'test-frame-{i:02d}.jpg'),composed)
    checks.append({'frame':i,'homography_inliers':inliers,'median_flow_px':float(np.median(np.linalg.norm(flow,axis=2)))})
    if i%15==0: print(f'Composited {i+1}/{len(frames)}',flush=True)
# Retain actual filmed motion; slow this continuous 2.37 s shot to exactly 3 s.
indices=np.rint(np.linspace(0,len(results)-1,72)).astype(int)
output=out/'santos-teste-3s-360x640.mp4'
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
cmd=[ffmpeg,'-hide_banner','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo','-s',f'{w}x{h}','-pix_fmt','bgr24','-r','24','-i','pipe:0','-ss','9.9','-i',source,'-map','0:v:0','-map','1:a:0?','-c:v','libx264','-preset','medium','-crf','24','-pix_fmt','yuv420p','-af',f'atempo={len(frames)/90:.8f}','-c:a','aac','-b:a','96k','-t','3','-movflags','+faststart',str(output)]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
for i in indices:
    proc.stdin.write(results[i].tobytes())
proc.stdin.close()
err=proc.stderr.read().decode()
code=proc.wait()
if code: raise RuntimeError(err)
report={'method':'Motion-tracked local video composite from an imagegen-edited reference frame. Original source camera motion and changing perspective retained.','keyframe_source':str(key_source),'source_start_seconds':9.9,'source_end_seconds':9.9+len(frames)/30,'source_speed_ratio':len(frames)/90,'output_seconds':3,'output_fps':24,'output_dimensions':[w,h],'output_file':str(output),'checks':checks}
(out/'render-details.json').write_text(json.dumps(report,indent=2))
cv2.imwrite(str(out/'test-contact-sheet.jpg'),np.hstack([results[0],results[ref_index],results[-1]]))
print('OUTPUT',output,'BYTES',output.stat().st_size,flush=True)
