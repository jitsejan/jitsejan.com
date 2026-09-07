Title: Reconstructing a dragged-down WordPress site with AI, GitHub Pages, and Cloudflare
Date: 2026-02-23 04:45
Modified: 2026-02-23 04:45
Category: posts
Tags: Cloudflare, Github Pages, WordPress, static website, AI
Slug: reconstructing-wordpress-site-with-ai
Authors: Jitse-Jan
Summary: A technical breakdown of how I migrated a WordPress site to a fast, cost-effective static site using AI, GitHub Pages, and Cloudflare.

When it was time to renew the domain for my friend medical practice in Germany, we were exactly two weeks late. My web host, SiteGround, didn't just want the usual 14 GBP for the renewal—they demanded an exorbitant 78 GBP late fee. After pushing back and citing some DENIC (the central registry for .de domains) regulations, they quickly crawled back and lowered it to the standard price. 

But this whole ordeal got me thinking: why am I paying for full WordPress hosting when the website is basically an online business card? With all the new ways of deploying static websites without hosting your own servers, it was the perfect time to optimize the setup.

## Digging up the past with the Web Archive
The original website was a simple WordPress instance. Instead of migrating the database or trying to export XML files, I took a more modern approach. I used the **Internet Archive (Wayback Machine)** to dig up the cached versions of the core pages: Home, Contact, and the all-important German Impressum.

I fed these findings directly into an AI assistant, instructing it to reconstruct the structure using pure, semantic HTML and a clean CSS stylesheet. No frameworks, no bloated PHP—just lightning-fast static files.

## The new hosting stack
With the HTML generated, here is the new infrastructure, pieced together using entirely free tiers:

1. **Domain Registration:** SiteGround (now used *purely* to hold the domain name, nothing else).
2. **DNS & Routing:** **Cloudflare**. SiteGround's nameservers were swapped out immediately.
3. **Hosting:** **GitHub Pages**. The repository is linked to my custom domain via Cloudflare, meaning updates are as simple as a `git push`.
4. **Email Routing:** I set up a fresh Google email address to act as the backend inbox. Cloudflare's free Email Routing forwards everything sent to `info@practice...` straight to that Gmail account.
5. **Sending Emails:** To reply from the custom domain without paying for Google Workspace, I integrated **Brevo**'s (formerly Sendinblue) SMTP server directly into the Gmail "Send mail as" settings. It easily handles outbound emails on the free plan.

### A note on Cloudflare email sending
While Cloudflare's inbound email forwarding works flawlessly, I am actively keeping an eye on their new Email Routing feature beta for *sending* emails. If they nail outbound sending directly through their dashboard, it could eventually remove the need for the Brevo SMTP workaround altogether.

Overall, it was an incredibly smooth experience to strip away a heavy CMS and replace it with a highly-performant, cost-effective stack. The site builds instantly, runs securely behind Cloudflare's proxy, and I'll never be held hostage by exorbitant hosting fees again.
