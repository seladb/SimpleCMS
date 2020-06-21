import React from "react"
import { Link } from "gatsby"
import Layout from "../components/layout"
import formatDate from "../utils/utils"

export default ({data}) => {
  console.log(data)
  return (  
    <Layout>
      <h1>{data.allBlogPostsQuery.allBlogPosts.edges[0].node.title}</h1>
      <div>By <Link to={`/${data.allBlogPostsQuery.allBlogPosts.edges[0].node.writer.username}`}>@{data.allBlogPostsQuery.allBlogPosts.edges[0].node.writer.username}</Link></div>
      <div>Published: {formatDate(data.allBlogPostsQuery.allBlogPosts.edges[0].node.published)}</div>
      <p></p>
      <p>{data.allBlogPostsQuery.allBlogPosts.edges[0].node.content}</p>
    </Layout>
  )
}

export const query = graphql`
  query ($id: ID!) {
    allBlogPostsQuery {
      allBlogPosts (id: $id) {
        edges {
          node {
            title
            content
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