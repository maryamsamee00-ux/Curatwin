# CuraTwin Vercel Deployment Guide

This guide will give CuraTwin a permanent public URL like `curatwin.vercel.app`.

## Step 1: Create a free Vercel account

1. Open your browser and go to **https://vercel.com/signup**
2. Choose one option:
   - **Continue with GitHub** (recommended — fastest)
   - **Continue with Google**
   - **Continue with Email**
3. If you use email, check your inbox and click the verification link.

## Step 2: Install the Vercel CLI

```bash
npm install -g vercel
```

## Step 3: Log in from the terminal

```bash
cd curatwin
vercel login
```

The terminal will show a message like:
`> Success! Token stored in ~/.vercel/auth.json`
(Or it may open your browser to confirm — click **Authorize**.)

## Step 4: Deploy to production

```bash
vercel --prod --yes
```

Wait 2-3 minutes. The output will end with a permanent URL like:

```
Production: https://curatwin-abc123.vercel.app
```

## Step 5: Test the live site

Open the URL in your browser and check:
- Landing page loads
- Register a new account
- Login works
- Dashboard shows your Digital Twin
- Submit telemetry and see the stress score update

## Important notes

- The free Vercel plan is enough for this project.
- Set environment variables (`SECRET_KEY`, `DATABASE_URL`) in the Vercel dashboard under **Settings > Environment Variables**.
- For persistent data, connect a Neon Postgres database via the Vercel integration.
- Do not share your Vercel login token or auth files with anyone.
