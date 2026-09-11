module.exports = function (eleventyConfig) {
  // Static assets copied as-is to the output
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy("src/js");
  eleventyConfig.addPassthroughCopy("src/images");
  eleventyConfig.addPassthroughCopy("admin");
  eleventyConfig.addPassthroughCopy("src/robots.txt");
  eleventyConfig.addPassthroughCopy("src/ads.txt");
  eleventyConfig.addPassthroughCopy({ "src/favicon.svg": "favicon.svg" });

  // All wallpapers, newest first
  eleventyConfig.addCollection("wallpapers", (api) =>
    api.getFilteredByGlob("src/wallpapers/*.md").sort((a, b) => b.date - a.date)
  );

  eleventyConfig.addCollection("featuredWallpapers", (api) =>
    api
      .getFilteredByGlob("src/wallpapers/*.md")
      .filter((item) => item.data.featured)
      .sort((a, b) => b.date - a.date)
  );

  // Filter helpers usable in templates
  eleventyConfig.addFilter("byCategory", (items, categorySlug) =>
    (items || []).filter((item) => item.data.category === categorySlug)
  );

  eleventyConfig.addFilter("limit", (items, count) => (items || []).slice(0, count));

  eleventyConfig.addFilter("countInCategory", (items, categorySlug) =>
    (items || []).filter((item) => item.data.category === categorySlug).length
  );

  eleventyConfig.addShortcode("year", () => `${new Date().getFullYear()}`);

  eleventyConfig.addFilter("readableDate", (dateObj) => {
    return new Date(dateObj).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  });

  return {
    dir: {
      input: "src",
      includes: "_includes",
      data: "_data",
      output: "_site",
    },
  };
};
