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
  const ServerQuery = await graphql(`
  {
    serverQuery {
      allBlogPosts {
        edges {
          node {
            id
          }
        }
      }
      allUsers {
        username
      }
    }
  }
  `)
  if (ServerQuery.errors) {
    reporter.panicOnBuild(`Error while running BlogPost GraphQL query.`)
    return
  }
  const BlogPosts = ServerQuery.data.serverQuery.allBlogPosts.edges
  BlogPosts.forEach(post => {
    createPage({
      path: `/${decodeBlogPostId(post.node.id)}`,
      component: BlogPostTemplate,
      context: {
        id: post.node.id,
      },
    })
  })
  const Users = ServerQuery.data.serverQuery.allUsers
  Users.forEach(user => {
    createPage({
      path: `/${user.username}`,
      component: PageTemplate,
      context: {
        username: user.username
      }
    })
  })
}
