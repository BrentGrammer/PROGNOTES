# SEO

## SEO in SPA (Client rendered) Applications

- One drawback of client-side rendering is how search engine bots like Googlebot access content. Googlebot has something called a second wave of indexing which means the HTML of a page is crawled and indexed first. The bots then come back to render the JavaScript when resources become available. This two-phased approach means that sometimes, JavaScript content can be missed, and not included in Google’s index.

### Generating a sitemap

- place the file in the `public` folder: `/public/sitemap.xml`
- Enter the site map xml address into Google Search Console (https://mysite.com/sitemap.xml)
- Use Screaming Frog to generate an xml sitemap
- Can use packages for react-router client side routing sitemap generation

### Social media linking

- Setting up Open Graph meta tags on your page is the best way to integrate the website nicely with social networks. This is something that is easy to do if you have previous experience with meta tags. see [link](https://kruschecompany.com/seo-tips-and-tricks-for-single-page-web-applications/#:~:text=Single%20Page%20Application%20SEO%20Sitemap.xml%20example%3A,-%3C%3F&text=However%2C%20your%20site%20will%20certainly,than%20if%20you%20don't.)

```
<head>
  <meat property="og:title" content="Some Title"/>
  <meat property="og:description" content="Short description"/>
  <meat property="og:type" content="article"/>
  <meat property="og:image" content="https://example.com/progressive/image.jpg"/>
  <meat property="og:url" content="https://example.com/current-url"/>
</head>
```

- Other social media apps like Twitter have their own variety of these tags as well etc.

### Canonical tag

- if you have a few similar pieces of content, which can confuse Google as to which to serve (sometimes resulting in none of the pages with duplicate content being very visible in the SERPs – search engine results pages) you choose one version and make it “canonical”. Search engines will then focus on your chosen piece of content, largely ignoring the other duplicate or similar instances.
- Ideally, you want to set the rel="canonical" tag to the canonical URL of the current content, not just the main domain. This is important for SEO because search engines need to understand which URL represents the current content. If you always set it to the main domain, you might run into issues with duplicate content.
- Dynamically Setting Canonical URLs: To handle the dynamic nature of SPAs, you would indeed use JavaScript to dynamically set the rel="canonical" tag based on the current URL in the user's browser. This ensures that the canonical tag reflects the URL of the current content being displayed within the SPA.
  - Can use packages like `helmet` to help with this.
- canonical and ‘sitemap.xml’s URLs must be the same!
