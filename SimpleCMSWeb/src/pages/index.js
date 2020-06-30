import React from "react"

import Layout from "../components/layout"
import SEO from "../components/seo"
import BlogPostSummary from "../components/blogPostSummary"

export default ({data}) => (
  <Layout>
    <SEO title="Page two" />
    {data.serverQuery.allBlogPosts.edges.map(({node}) => {
      return (
        <BlogPostSummary data={node} />
      )
    })}
  </Layout>
)

export const query = graphql`
  query {
    serverQuery {
      allBlogPosts {
        edges {
          node {
            id
            title
            published
            writer {
              username
            }
            likeSet {
              id
            }
            commentSet {
              id
            }
          }
        }
      }
    }
  }
`
