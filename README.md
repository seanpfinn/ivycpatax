# Ivy Tax & Business — redesign proposal

[![Ivy Tax social preview: the Ivy T mark draws itself as a route map with a compliance line and a strategy line, and trains run both routes](og/og-preview.gif)](og/og-video.mp4)

<sub>Social preview video, 1200×630 at 60 fps. Click for the full-quality mp4.</sub>

A single-file concept homepage for **ivycpatax.com**, the website of Ivy Tax & Business Inc. (安腾会计), a CPA-led tax and advisory firm at 6800 Jericho Tpke, Suite 120W, Syosset, NY 11791. Replaces the current WordPress site (Impreza theme + Elementor + Slider Revolution).

## Concept

**Every dollar has a route.** The firm's logo is two interlocking spirals of bars forming a T, with a small red square at the start. The hero turns that exact mark into a transit map of a year with Ivy: the outer spiral becomes the **Compliance line** (monthly books → payroll reviewed → quarterly filings → year-end close → returns filed) and the inner spiral becomes the **Strategy line** (structural assessment → written strategy → year-round implementation → ongoing monitoring). The red square is labeled *YOU*: both lines start with the client. On load the lines draw in, stations pop, and two trains run the routes. "Which route is yours?" chips (S-Corp owner, real estate investor, online seller, K-1s, IRS letter, starting a business) light up the stops that apply and open the matching tab below.

The rest of the page keeps the transit language: line-colored eyebrows, a four-stop process line, pricing as "fares, posted up front," and the 13 town pages laid out as **Local stops** on a line from Syosset. The S-Corp differentiator gets its own set piece: **"One profit. Two ways out."**, a salary-vs-distributions slider that shows payroll tax on the salary portion, with the scrutiny and over-payment ends marked.

The firm's own tagline is the H1: *Precision tax planning, profound savings.*

**Carried over from the live brand:** the T mark rebuilt exactly from the bars of `IVYCPA-TAX-LOGO-.png` (measured in the browser), its indigo `#2E3192` and red square, the Ivy Smart Tax orange, Poppins (the live site's font), and 安腾会计 in the lockup.

## Audit summary (live site, November 2026)

1. **The site contradicts itself on whether the first step is free.** Every page's header says "Free Discovery Call" and "Free Consultation"; the Tax Reduction page says "start with a complimentary diagnostic review," then its FAQ says "Tax reduction diagnostics and evaluations are not free" (stated twice), and the IRS Notice FAQ repeats "Diagnostic reviews are not free" three times. → Decide what's free (the call?) and what's paid (the diagnostic), and say it once. *This build says "Book a discovery call" and never says free.*
2. **Internal SEO notes are published as headings.** The Tax Reduction page has an H2 "Additional Tax Reduction Questions (AnswerThePublic – Q13–Q19)," and the IRS Notice page has "IRS Notice FAQ (Q1–Q12)," "(AnswerThePublic – Q13–Q20)" and the typo "RS Notice – Frequently Asked Questions." → Remove the keyword-tool labels; fix the typo.
3. **The "Pricing" page is titled "Form."** Its title is "Form - Ivy Tax & Business Inc.", `og:title` is "Form", its description is about "submitting essential tax forms," and the share image is a 512px logo. The best pricing story on the site ($350/mo advisory, $280/mo bookkeeping, $500 and $1,600 returns) is invisible in search and shares. → Rename to Pricing; put starting prices on the homepage. *Done.*
4. **Ten H1s on the homepage**, including "Comprehensive CPA & Accounting Services," "Schedule a Consultation," "Frequently Asked Questions," and "Find an Accountant in Long Island, New York" (twice). `og:title` is "Home new-EN" (and "Home new- CN" on /zh/). → One H1; real share title.
5. **The CPA is never named.** "CPA-led" and "licensed CPA supervision" appear on every page, but no name, license number or photo. (A Syosset Chamber listing names Fiona Zou.) → Add the CPA's name, NY license and a portrait to About and the homepage.
6. **The tax-reduction "How it works" is scrambled.** Two lists are interleaved, so "01 LLC owners, S-Corp owners…" and "01 Meet your Certified Tax Coach" alternate, then the steps repeat, then a different four-step process follows. It also claims "average savings… over $14,000 per year" with no source. → One process (used here); source or cut the $14,000 figure.
7. **English footers link to Chinese pages.** On every English page the footer's "Company Establishment," "Company tax return," "Personal Tax"… go to `/zh/` URLs; "Serve"/"Service" and "Twitter"/"Instagram" are unlinked labels; "Copyright 2021." → Language-matched links; computed copyright.
8. **Dead and inconsistent links.** "Free Resources," "Client Support Center" and "Helpful Client FAQs" are `href="#"`; the Services page links to non-`/en/` paths and its "Proactive Tax Planning" card is `#`; the consult page slug is `/free-consulation/` with the H1 "Free Consulation"; the e-book link is `http://`; one Chinese tracker link ends in `mileagetrackeracker`. The hero slider's "Specialize in complex tax situations…" button goes to the **Payment Center**. → Fix all; redirect the misspelled slug.
9. **Stock imagery passed off as the firm's own.** The homepage hero is a Manhattan skyline for a Syosset firm, and the "about" photos are stock meeting shots saved as `WhatsApp-Image-2025-02-18…jpg`, which is also the homepage `og:image`. → Real office and team photos; no stock in this build.
10. **Three phone numbers, no hours.** Contact lists 516-344-8065, 718-801-8060 (text) and 516-368-3747; other pages list two. No office hours anywhere. → Confirm the third line; publish hours. *This build shows "By appointment."*
11. **Heavy, duplicated tech.** The nav markup ships six times per page; MailerLite and Mailchimp both load; Slider Revolution 6.3.6 (2020), Elementor and the Impreza theme stack on one page; four Google Maps iframes (one is just "USA") load on the homepage. → One nav, one newsletter tool, no slider, a single map link.
12. **The bilingual service is a footnote.** Chinese support (a Chinese-speaking line, WeChat) appears only in the footer. → Promoted to the header strip, proof band, form (language choice), FAQ and call sheet.

## What's in the redesign

- **Route-map hero** (`<figure>`): generated SVG from the logo's own geometry, `stroke-dashoffset` line draws, spring-in stations, rAF trains that pause off screen; an HTML legend carries the content (the SVG is `aria-hidden`), with an `aria-live` readout. Six `aria-pressed` chips filter the stops, select the matching tab and preselect the form's service.
- Proof band: CPA-led · Year-round · 中文 & English · All 50 states · Tax coach trained.
- **"Start with what's in front of you"** tabs (`role=tablist`, arrow/Home/End keys, `aria-selected`, `hidden` panels, tallest panel reserved; horizontal swipe row with `aria-orientation` switched on phones): S-Corp · real estate · online seller · K-1s & 1099s · IRS/state letter · starting a business. Each lists services from the live pages, a "good to know" card from the site's FAQs, a starting price and links to the existing pages.
- "Most firms file returns. We plan the structure." comparison; the four-stop strategy process with real timings (1–2 weeks, 2–4 weeks) and the site's honest "not a fit for" list.
- **S-Corp split tool**: illustrative $150,000 profit, `range` input with `aria-valuetext`, animated bar, three-zone note (reserved height, `aria-live`) and a not-tax-advice line. Plays a short sweep when scrolled into view.
- Fares (four starting prices from the pricing page), Ivy Smart Tax Academy shelf (the five Gumroad products + videos), seven FAQs, Visit with both phone lines, email, WeChat ID, Local stops linking all 13 town pages, and a discovery-call form with a language choice.
- **Mobile tab bar** (≤980px): T mark · Services · Pricing · Call (sheet: English, 中文, text) · **Book a call** pill ("Book" under 430px), scroll-spy on Services and Pricing. Rises after the map finishes drawing, stays visible through the footer.

## Spacing & performance

- Spacing tokens 8/12/16/24/32/48/64px and fluid section padding `clamp(64px,9vw,112px)`; type tokens `--lh-body:1.65`, `--track-label:.12em`.
- One `backdrop-filter` (sticky header), one rAF-throttled scroll handler using `getBoundingClientRect()` (reveals, header, scroll-spy, map visibility, S-Corp sweep), pre-tinted SVG grain, no blend modes. Fonts: Source Serif 4 600 + italic (display, optical sizing), Poppins 400/500/600, JetBrains Mono 500, and Noto Sans SC loaded with `text=` for only the Chinese characters used.
- Load sequence: header slides down → headline lines rise from masks → lede and chips → map card springs in → ghost mark fades up → compliance line draws, then strategy line → stations pop as the lines pass → trains depart → tab bar rises last. Gated on `load` + `document.fonts.ready` + 250ms with a 4s fallback; reduced motion shows the finished map with no trains; without JS everything is visible.
- Verified at 1440, 390 and 360px: no horizontal overflow, no console errors, **axe-core (WCAG 2.2 AA + best practice): 0 violations**, tab bar visible at hero/mid-page/footer (with and without reduced motion) and hidden on desktop, exactly one selected tab-bar item in Services and Pricing and none elsewhere, tab keys and chips working.

## Notes before launch

- **Logo:** the T mark is rebuilt exactly from the live PNG's bars; the lockup text is outlined from Poppins and Noto Sans SC. Swap in the master vector if one exists.
- **No client photos are used**, because the live site only has stock. A portrait of the CPA, the team and the Jericho Tpke office are the most valuable shoot.
- **No invented claims.** Services, prices, timings, the "not a fit" list, FAQ answers, phones, email (decoded from the Cloudflare-protected link), WeChat ID, towns and Academy products all come from the live English and Chinese pages. The route map's stops are the firm's own process and service language; the S-Corp tool is labeled illustrative.
- **Confirm before launch:** whether the discovery call is free and the diagnostic paid; the CPA's name and license; office hours; whether 516-368-3747 is still in service; the "$14,000 average savings" claim (left off); Certified Tax Coach status; the "all 50 states" wording.
- **Form:** demo submit handler. Wire it to the office inbox (Formspree or a serverless function) and keep one newsletter tool.
- **Chinese version:** `/zh/` stays linked; a matching Chinese build of this page is the natural next step.

## Files

- `index.html` — the page (inline CSS and JS; Google Fonts is the only external request)
- `logo.svg`, `favicon.svg`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`, `site.webmanifest`
- `og/og-video.html` — 1200×630 composition driven by a deterministic `render(t)`
- `og/og-video.mp4` — 8 s, 60 fps H.264; `og/og-image.jpg` — final held frame; `og/og-preview.gif` — 720px preview
- `build/` — `logo.py` (mark + lockup), `template.html` + `build.py` (map SVG, FAQ, JSON-LD → `index.html`), `og_build.py`

## Social preview & metadata

Beats: the grid fades up → the route-map card springs in with the ghost T → brand, eyebrow and "Precision tax / planning, / *profound savings*." rise → the compliance line draws, then the strategy line, stations popping as they pass → the ticker (phones, address, services, starting prices) slides in and moves exactly 1px per frame (verified on the encoded file) → trains run both lines → the mobile tab bar rises last, then holds.

`og:url`, the canonical, OG/Twitter images, the video and JSON-LD (`WebSite`, `WebPage`, `ImageObject`, `VideoObject`, `AccountingService` with both language contact points and the offer catalog, `FAQPage`) use the live deploy, **https://ivycpatax.vercel.app/** (Vercel project `ivycpatax`, team Finrez). At launch, rebuild with `SITE=https://ivycpatax.com/ python3 build/build.py`, then run the URL through the Facebook Sharing Debugger to clear cached previews.
