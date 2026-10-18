# 成图与局部改稿提示词

## 工具输入

使用已有内置图像工具；模板不是 API 参数。调用前看清输入照片，核对实际输入顺序。不能只在提示词列路径，却没有真正附图。

本地文件走工具支持的本地引用字段；聊天附件走近期图片引用机制。窗口不足时优先用可访问本地路径；两种方式都无法包含全部图片时请求补附必要图片，不静默少传。工具不支持的参数不能臆造。

## 单页模板

替换全部大括号，没有的字段删除。只选择一种适合当前内容的版式。

```text
Use case: compositing — personal photo scrapbook journal.
Create ONE finished, flat, edge-to-edge Chinese scrapbook plog page.
Target aspect ratio: {3:4 or user ratio}; high resolution, ideally {1536x2048 or matching dimensions}. The page itself fills the canvas. It is not a photograph of a notebook on a desk.

INPUT MAP — match the actual attached image order:
Image 1 = P1, USER CONTENT: {visible scene, protected subject, assigned role}.
Image 2 = P2, USER CONTENT: {...}.
Image 3 = P3, USER CONTENT: {...}.
{Image 4 = P4, USER CONTENT: ...}
{Optional final image = S1, STYLE ONLY: use only paper, hierarchy and annotation rhythm. Do not transfer its people, photos, objects, exact text, signature or watermark.}

PHOTO INVARIANTS:
Use the supplied photographs as source content. Keep the same recognizable people, facial features, clothing, poses, actions, objects and actual environments. Preserve candid phone-photo character and realistic colors. No face swapping, beauty retouching, synthetic replacement scenes, added people or invented documentary details. Use all required sources {P1,P2,...}. Do not invent additional photo panels. Any cutout comes from its stated source, not a new event.
PHOTO COVERAGE: the user supplied {N} source photos. This page must contain {the listed sources assigned to this page}, each visibly traceable to its source. Do not choose to omit sources for aesthetics. {If multi-page was announced, name this page and its assigned sources.}

STORY:
{One sentence grounded in user-confirmed facts and visible photos; no guessed dates, places, relationships or thoughts.}

LAYOUT:
{One concrete composition: hero source, support sources, relative sizes, positions, viewing order, crop protection and any source-derived cutout.}
Keep one clear visual anchor or distinct story groups. Use subtle size variation and useful breathing room. Keep each annotation beside its corresponding photo. Photo area is dominant, roughly {appropriate range}% of the page. Do not crop or cover faces, hands and key objects.
FREE COLLAGE RHYTHM: vary photo sizes, local angles, offsets and spacing; allow small overlaps on photo margins or empty backgrounds, a cutout crossing a paper/photo edge, and notes fitting into organic gaps. Keep an asymmetric but readable photo cluster. Avoid ruler-straight rows, equal gutters, identical card modules or every photo tilted the same way. Do not simply rotate an otherwise rigid grid. These relationships adapt to actual sources; do not mechanically copy wireframe coordinates. Preserve enough visible area to recognize every required source. {User-requested orderly layouts override this default.}

VISUAL LANGUAGE:
Light {warm-white/beige/kraft} paper with subtle texture. Casual black Chinese pen handwriting, natural line breaks and clear hierarchy. Emphasis colors sampled from photos: {one or two}. Restrained paper overlaps, fine white edges or thin hand-drawn borders. {One or two content-related doodles}. Clear and expressive handmade feeling, not random scatter. Preserve source colors; no overall sepia filter.
Use {specific title/keyword lettering treatment} and {a small purposeful set of sticker motifs and their locations} at selected structural junctions. Keep body copy simple and readable; no font change on every line. RESERVE CALM PAPER: plan one or two connected, visibly empty paper areas beside the title, between photo groups or outside the main silhouette. Roughly 15–25% calm paper is a flexible starting point, not a measured quota; photo borders and paper covered in stickers or captions do not count. Keep these areas free of text, stickers, arrows, colored blocks and scattered marks. Decorate selected gaps, leaving others untouched; do not wrap the whole page in a continuous decorative border. Aim for a little breathing room without a large empty block or blank footer. If crowded, reduce repeated decorations and oversized title lettering first, preserving every assigned source photo at a readable size.

EXACT CHINESE TEXT — render only these strings, verbatim:
Title at {location}: "{title}".
P1 annotation near P1: "{caption1}".
P2 annotation near P2: "{caption2}".
P3 annotation near P3: "{caption3}".
{P4 annotation: ...}
{Optional closing line: "...".}
{Optional confirmed date: "...".}
No extra copy, automatic timestamps, invented labels, prices, locations or signatures. Keep Chinese legible on a phone; shorten copy rather than shrinking it into tiny decorative text.

AVOID:
Default equal four-cell catalog grid with identical frames and caption positions; generic sun-leaf-coffee decoration set; wooden tabletop, notebook spine, surrounding stationery; heavy stains or noise; decoration overload; glossy poster/slide UI; generated new memories; extra people/photo panels; borrowing the reference creator's family, story, fixed title or signature. {Adjust these defaults when the user explicitly asks for one.}
```

## 只修人物区域

重新附成图与对应原照，明确成图是编辑目标、原照是身份/场景依据。不要只说“修好人脸”。

```text
Edit the scrapbook in Image 1. Image 2 is the user's original P2 photo and the only content authority for its people, pose, clothes and scene. Correct only the P2 photo region to match the source. Keep page layout, other photos, Chinese text, paper and decorations unchanged. Do not introduce another person or a new pose.
```

修复仍不稳定时，不能声称保真；按入口的原图排版分支处理。

## 只修错字

```text
Edit only the annotation beside P3: replace "{wrong}" with exactly "{correct}". Match existing casual black Chinese handwriting. Preserve every photograph, face, page geometry, paper, other text and decoration. Add no new text.
```

## 调整主次

```text
Keep the supplied photographs and approved text. Make P{n} the visual anchor, larger than support photos; group detail photos near their local annotations; remove two redundant decorations; keep one calm paper area. Preserve actual people and scenes. Do not create more photos or change the factual story.
```

局部修改不无故改变整页。若工具不能稳定保留其余区域，明确实际变化，不能把全面重绘说成局部不变。
