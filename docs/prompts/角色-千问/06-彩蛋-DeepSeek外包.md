# 彩蛋：DeepSeek 偷懒，把活外包给千问（5 张）

出现在 **DeepSeek** 那里：DeepSeek 偷懒去了，戴着她的女仆头饰站在那儿干活的其实是千问（名牌显示「DeepSeek？」）。
你点一下，千问笑着承认：「被发现啦～她说今天想睡懒觉，我就接下来了。」然后把做好的活交回给睡眼惺忪的 DeepSeek，顺手塞她一杯奶茶。
没人点的话，千问把活做完，留下一杯奶茶悄悄走掉。
梗：DeepSeek 设定里「其实有点懒」+ 千问有钱、大方、爱请客。

**附件两张，说明哪张是谁**：`docs/prompts/ref-qwen.webp`（千问）和 `docs/prompts/ref-deepseek.webp`（DeepSeek，女仆装原版）。
画好放进 `characters/egg-deepseek-qwen/raw/`，文件名 `pop` / `pretend` / `caught` / `bye` / `escape`。

```
Two images are attached. The FIRST is Qwen (the gentle rich young lady with periwinkle-blue hair and a fan). The SECOND is DeepSeek (the blue whale maid girl). Draw desktop-pet sprites for a short "visitor" scene.

FORMAT RULES (every image):
- Pure flat white background (#FFFFFF). Nothing else: no floor, no cast shadow, no glow, no vignette, no frame.
- No text, no letters, no numbers, no speech bubbles, no symbols floating in the air. The app draws all effects itself.
- Exactly one character (except bye.png, see below), full body, standing, centered. Head near the top and feet near the bottom; she fills about 90% of the image height.
- A continuous, closed dark outline around the whole silhouette, so no white or pale part ever touches the white background directly.
- Same art style as the references: clean lineart, flat two-tone cel shading, soft palette, chibi about 2.5 heads tall, big head, long flowing hair.
- Square image, 1024x1024 or larger. One image per file, saved under the exact filename given.
- Every prop touches a hand; nothing floats.

CHARACTER LOCK — Qwen, the anime-girl personification of Qwen (Alibaba's AI), a gentle and generous young lady from a wealthy family.
Personality: warm, gracious, generous and well-mannered; she loves treating everyone (buying milk tea for the whole office is normal to her) and thinks sharing good things is simply natural. Never arrogant, never mean: a soft, kind "rich big-sister" smile. A little sheltered and easygoing about money, which makes her endearing rather than snobbish.
Keep exactly:
- Very long, wavy periwinkle-blue hair down past the waist, side-swept bangs, a braided crown on her left side (viewer's right) and one long braid falling over her left shoulder (viewer's right).
- Big round violet-blue eyes with bright highlights, soft pink blush.
- A small dark-navy hat worn tilted on the viewer's left side of her head, with a white fur trim, a white ribbon bow, a gold-framed round blue emblem (a white stylized knot shape) and small blue tassels.
- Gold drop earrings with small blue gems.
- White mandarin-collar dress with gold frog buttons and faint white floral embroidery; a dark-navy wide-sleeved over-robe with gold Greek-key borders; a blue front skirt panel with a blue ribbon bow and a round emblem brooch at the waist; blue tassels with gold knots hanging from the waist; a white frilly underskirt; white gloves; navy heels with small gold anklet charms.
- Signature prop: a blue folding fan with gold ribs and a white leaf pattern. Keep it in her hand in most poses unless the pose says otherwise.
- Secondary prop: a small white-and-gold handbag with the same round emblem. Draw it ONLY when a pose mentions it.
Palette: periwinkle blue, dark navy, white and soft gold. Keep it elegant; no other strong colors.
How she shows emotion: gracefully, mostly with the fan. Laughing = fan raised to cover her mouth with smiling closed eyes; thinking = closed fan tapping her chin; shy = fan hiding the lower half of her face; pleased = fan opened with a gentle flourish; upset = fan snapped shut. Expressions are bright and open (like the reference's happy open-mouth smile), but always gentle and lady-like, never loud.

SECOND CHARACTER (only in bye.png) — DeepSeek, the blue whale maid girl. Keep exactly: long wavy hair, deep navy fading to bright blue at the tips, one curled ahoge; a large white frilly maid headdress; dark navy whale-fin ears; a light-blue ribbon bow on her right side (viewer's right); big round bright-blue eyes; navy maid dress with a white frilly apron (small navy whale emblem), navy skirt with gold vine embroidery; a big dark-navy whale tail curling out on the viewer's right. Personality: cheerful, a bit lazy, sweet-talking.

DISGUISE (pop / pretend / escape): Qwen is standing in for DeepSeek. Over her usual outfit she wears DeepSeek's large white frilly maid headdress (it replaces her own hat, which she holds or has tucked away) and a small white frilly apron with a tiny navy whale emblem tied over her dress. Her hair, braid, face, fan and the rest of her outfit stay exactly as Qwen.

EGG POSES:
pop.png     — Qwen in the disguise steps in politely, holding a slim white laptop (closed) against her chest with one arm, the closed fan in the other hand, a gracious "leave it to me~" smile, as if she just arrived to take over the shift.
pretend.png — Qwen in the disguise working seriously as DeepSeek would: holding the open white laptop on one forearm and typing with the other hand, a cup of milk tea (clear cup, dome lid, wide straw, tapioca pearls, no logo) balanced on the closed laptop corner touching her hand, a focused but gentle face, pretending nothing is unusual.
caught.png  — Found out! Qwen pulls the maid headdress off with one hand (holding it, her own hat now back on her head), the open fan raised to cover her mouth with the other hand, eyes closed in an amused, embarrassed giggle ("you caught me~"), a light blush. Only Qwen is drawn.
bye.png     — Handing the work back. Exception to "exactly one character": both are drawn, fully inside the image, their outlines touching so they form one connected group. Qwen (in her normal outfit, own hat back on) on the viewer's left holds out the closed white laptop and a cup of milk tea toward DeepSeek with a warm "all done, and this one's on me~" smile. DeepSeek on the viewer's right has clearly just woken up: hair slightly messy, ahoge flopped, one eye still half-closed, rubbing her eye with one hand and happily reaching for the milk tea with the other, whale tail swaying.
escape.png  — Nobody noticed, so Qwen finishes up and slips away: body turned slightly toward the viewer's LEFT as if walking off, face still toward the viewer, the maid headdress hooked on her wrist and the closed laptop under her arm, waving goodbye with the open fan, a gentle satisfied smile. Only Qwen is drawn.
```

看稿：pop / pretend 一眼看得出是「戴着 DeepSeek 头饰的千问」（蓝紫长卷发、辫子、扇子都在）；bye 两人轮廓连在一起（不连着的会被导入工具当杂点删掉），DeepSeek 刚睡醒的样子；奶茶杯上没有字和标志。
