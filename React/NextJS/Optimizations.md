# Optimizations

## Images

- can use the `<Image>` [component](https://nextjs.org/docs/pages/api-reference/components/image) from the `next/image` package
- The image component automatically compresses and resizes images based on the device size.
  - always use this over the standard <img> tag.
  - will convert images like jpg to webp which is a new format compatible with browsers and far smaller in size

### Remote Images

- You need to [register the domain](https://nextjs.org/docs/pages/api-reference/components/image#remotepatterns) for the image in the Next configuration (next.config.js) file
- Always provide a dimension with remote images in the <Image /> component since Next.js does not know the image size ahead of fetching. (for local images since they are imported from a folder it knows the dimensions)

```javascript
<Image
  src="https://bit.ly/react-cover"
  alt="my react cover image"
  width={300}
  height={170}
/>
```

- To make images responsive, instead of setting width and height pass the `fill` property (which is a boolean)
- use objectFit: cover to fix aspect ratio problems, 'contain' will do the same but make the image fit in the container.
  - most of the time you want to use cover
- when using `fill` to show responsive images you also need to provide `sizes`.
  - determines how much width of the viewport the image takes (ex: background image always takes `100vw`)
  - you can also use special strings that look like a media query: `(condition) width, (condition) width`
    - Ex: `"(max-width: 480px) 100vw, (max-width: 768px) 50vw, 33vw"`
      - mobile (480px) image should take up one col, tablet (768) should take up 2 cols and everything else larger should take up 3 cols.

```javascript
<Image
  src="https://bit.ly/react-cover"
  alt="my react cover image"
  fill // when using fill parent needs position of relative, absolute or fixed
  // style={{ objectFit: 'contain'}}
  className="object-cover" // use tailwind instead
  sizes="100vw"
  // sizes="(max-width: 480px) 100vw, (max-width: 768px) 50vw, 33vw"
  quality={75} // 75 works for most cases, background images could be 100 for highest quality
  priority // boolean - whether should load above the fold. Images are lazy loaded by default. use if you have images that need to be visible on first load
/>
```

```javascript
// add one or more domains where you are allowed  to serve external images from. Done for security to prevent someone taking advantage of the endpoint that next.js exposes automatically for optimized images.
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "bit.ly",
        // port: "", optional port for the link
        // pathname: "/account123/**", // should be as specific as possible here for security
      },
    ],
  },
};
```

## Adding Third Party Scripts

- i.e. google analytics for example
- If script is needed on all pages, then add it to the root layout, otherwise add it to the pages that need it.
- use `<Script>` component from the `next/script` package provided by Nest.js
  - Has strategy prop:
    - `beforeInteractive` - script is loaded before NextJS injects any client side code (hydration). Use only for critical scripts like bot detectors or cookie consent managers.
    - `afterInteractive` - script is loaded after page is hydrated. Used for things like tag managers and analytics scripts.
    - `lazyOnload` - script is loaded after all resources on page have been fetched. useful for things like background scripts or low priority things like chat plugins or social media widgets.
    - `worker`
- It can be cleaner to take scripts and put them into a separate component to prevent cluttering up the component you call them in.

```javascript
const GoogleAnalyticsScript = () => {
  return (
    <>
      <Script
        async
        src="https://www.googletagmanager.com/gtag/js?id=youranalyticsid"
      />
      <Script id="googleanalyticsscript" strategy="afterInteractive">
        {/* if you get errors about unknown globals, then you can wrap the script in backticks and brackets - this is passing a script as a string which will be parsed as JS code*/}
        {`window.dataLayer = window.dataLayer || [];
        function gtag() {
          dataLayer.push(arguments);
        }
        gtag('js', new Date());
        gtag('config', 'G-E720JHXSJ1')`}
      </Script>
    </>
  );
};
```
