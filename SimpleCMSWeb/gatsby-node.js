/**
 * Implement Gatsby's Node APIs in this file.
 *
 * See: https://www.gatsbyjs.org/docs/node-apis/
 */

// You can delete this file if you're not using it

const path = require(`path`)

const decodeBlogPostId = (base64EncodedId) => {
    let buff = Buffer.from(base64EncodedId, 'base64');
    return buff.toString('ascii').split(':').pop();
}

exports.createPages = async ({ graphql, actions, reporter }) => {
  const { createPage } = actions
  const BlogPostTemplate = path.resolve("./src/templates/blogpost.js")
  const PageTemplate = path.resolve("./src/templates/page.js")
  const result = await graphql(`
  {
    allBlogPostsQuery {
      allBlogPosts {
        edges {
          node {
            id
            title
            published
            writer {
              username
              id
            }
          }
        }
      }
    }
  }
  `)
  if (result.errors) {
    reporter.panicOnBuild(`Error while running GraphQL query.`)
    return
  }
  const BlogPosts = result.data.allBlogPostsQuery.allBlogPosts.edges
  BlogPosts.forEach(post => {
    createPage({
      path: `/${decodeBlogPostId(post.node.id)}`,
      component: BlogPostTemplate,
      context: {
        id: post.node.id,
      },
    })
    const Pages = result.data.allBlogPostsQuery.allBlogPosts.edges
    Pages.forEach(page => {
      createPage({
        path: `/${page.node.writer.username}`,
        component: PageTemplate,
        context: {
          id: page.node.writer.id,
        },
      })
    })
  })
}
