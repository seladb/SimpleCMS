import React from "react"
import { Link } from "gatsby"

import Layout from "../components/layout"
import SEO from "../components/seo"
import formatDate from "../utils/utils"

export default ({data}) => (
  <Layout>
    <SEO title="Page two" />
    {data.allBlogPostsQuery.allBlogPosts.edges.map(({node}) => {
      return (
        <p key={node.id}>
          <Link to={atob(node.id).split(':').pop()}><h3>{node.title}</h3></Link>
          <div>By <Link to={node.writer.username}>@{node.writer.username}</Link></div>
          <div>Published: {formatDate(node.published)}</div>
        </p>
      )
    })}
  </Layout>
)

export const query = graphql`
  query {
    allBlogPostsQuery {
      allBlogPosts {
        edges {
          node {
            id
            title
            published
            writer {
              username
            }
          }
        }
      }
    }
  }
`
