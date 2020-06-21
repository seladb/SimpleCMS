module.exports = {
  siteMetadata: {
    title: `SimpleCMS`,
    description: `An example project to demonstrate the integration between Django and GraphQL`,
    author: `@seladb`,
  },
  plugins: [
    `gatsby-plugin-react-helmet`,
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `images`,
        path: `${__dirname}/src/images`,
      },
    },
    `gatsby-transformer-sharp`,
    `gatsby-plugin-sharp`,
    {
      resolve: `gatsby-plugin-manifest`,
      options: {
        name: `gatsby-starter-default`,
        short_name: `starter`,
        start_url: `/`,
        background_color: `#663399`,
        theme_color: `#663399`,
        display: `minimal-ui`,
        icon: `src/images/gatsby-icon.png`, // This path is relative to the root of the site.
      },
    },
    {
      resolve: "gatsby-source-graphql",
      options: {
        typeName: "BlogPostNodeConnection",
        fieldName: "allBlogPostsQuery",
        url: "http://127.0.0.1:8000/graphql/",
      },
    },
    // {
    //   resolve: "gatsby-plugin-extract-schema",
    //   options: {
    //     dest: `${__dirname}/all_schema.json`,
    //   },
    // },
  ],
}