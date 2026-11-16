---
project_id: achei-o-manto
updated_at: 2026-11-13
status: experimental
sources: [T-MANTO-VIDEO, F-MANTO-VIDEO-PREP, F-MANTO-VIDEO-RENDER, F-MANTO-VIDEO-CODE]
---

# Experimento: trocar a camisa no vídeo

Trabalho de futebol associado à frente de camisas, sem aplicação de identidade visual de marca comprovada. Não representa formato oficial do perfil.

## Pedido e sequência

O usuário forneceu `/Users/g.martins/Downloads/jersey.mp4` e pediu trocar a camisa pelo terceiro uniforme do Santos de 2026. Forneceu fotografias e a URL da Umbro como referência. Depois pediu textura e iluminação mais orgânicas, apontou aparência de camisa digital em cenário real e solicitou um teste de três segundos em baixa resolução.

As primeiras entregas foram imagens estáticas. Uma resposta intermediária disse depender de um editor externo; foi superada pela montagem local entregue posteriormente. Não exigir a instalação daquele serviço como condição atual apenas com base na resposta antiga.

## Resultado documentado

- Entrega: `output/santos-video-test/santos-teste-3s-360x640.mp4`.
- Duração de saída: 3 s; 360×640; 24 fps; 72 quadros de saída, conforme metadados locais.
- Origem: tomada contínua entre aproximadamente 9,9 e 12,2667 s do vídeo; trecho desacelerado com razão 0,7888889 para preencher 3 s.
- Método: quadro de referência editado por geração de imagem, máscara, rastreamento de movimento, deformação por fluxo óptico e transferência suave de variação de luz. O movimento vem da filmagem; não é apenas zoom numa foto.
- Código preservado: `output/santos-video-test/compose_test.py`; dependências: Python, OpenCV, NumPy, imageio_ffmpeg/FFmpeg.
- Materiais locais: quadro editado, máscara, referência de rastreamento, frames `.npy`, trecho original, frames de inspeção e folhas de contato.
- Metadados: `preparacao-do-teste.json` e `render-details.json`; o segundo registra verificações para 71 frames-fonte, remapeados para 72 frames de saída.

Esses dados vêm dos arquivos, da inspeção do código e do histórico. Esta consolidação não rerenderizou nem reavaliou visualmente cada frame. O teste não tem aprovação posterior do usuário registrada.

## Fidelidade pedida

Camisa preta Santos third 2026 conforme as referências: jacquard discreto, escudo e símbolos correspondentes, gola e detalhes brancos, sem patrocínio central. Preservar cabide, cenário, câmera, luz, dobras e perspectiva. Remover elementos da camisa original Tottenham/Nike/AIA. Usar as imagens oficiais indicadas pelo usuário antes de nova edição; o texto do prompt não substitui a ficha do produto.

## Limitações e retomada

- O resultado usa composição rastreada de um quadro; não comprova reconstrução física perfeita de tecido, oclusões ou detalhes durante todo o vídeo.
- O código contém caminhos absolutos para o original e uma imagem gerada fora do projeto; não é diretamente portátil. O quadro já salvo em `santos-video-keyframe.png` permite planejar uma adaptação, mas o código atual copia a fonte externa antes de renderizar.
- A chamada de áudio é opcional (`-map 1:a:0?`); não afirmar preservação de áudio sem inspecionar o arquivo final.
- Algumas referências apontam para Downloads e área temporária. Rechecar a disponibilidade antes de executar.
- Próxima etapa somente se solicitada: revisar movimento/tecido com o usuário, ajustar o teste e então dimensionar edição completa. Não registrar o vídeo inteiro como concluído.
