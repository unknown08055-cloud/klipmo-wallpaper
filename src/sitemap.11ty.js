class Sitemap {
  data() {
    return { permalink: "/sitemap.xml", eleventyExcludeFromCollections: true };
  }
  render(data) {
    const site = data.site;
    const urls = new Set(["/", "/wallpapers/", "/about/", "/contact/", "/privacy/", "/terms/", "/guide/live-wallpapers/"]);
    ((data.categoriesData && data.categoriesData.categories) || []).forEach((c) => urls.add(`/category/${c.slug}/`));
    (data.collections.wallpapers || []).forEach((w) => urls.add(w.url));
    const body = Array.from(urls)
      .map((u) => `  <url><loc>${site.url}${u}</loc></url>`)
      .join("\n");
    return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`;
  }
}
module.exports = Sitemap;
