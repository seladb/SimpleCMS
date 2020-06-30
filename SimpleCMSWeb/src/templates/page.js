import React from "react"

import Layout from "../components/layout"
import BlogPostSummary from "../components/blogPostSummary"

export default({data}) => {
  var firstName = data.serverQuery.allUsers[0].firstName
  var lastName = data.serverQuery.allUsers[0].lastName
  var username = data.serverQuery.allUsers[0].username
  return (
    <Layout>
      { firstName !== '' || lastName !== '' ?
        <h1>{[firstName, lastName].join(" ")} ({username})</h1>
        :
        <h1>{username}</h1>
      }
      {data.serverQuery.allUsers[0].blogpostSet.edges.map(({node}) => {
        return (
          <BlogPostSummary data={node} />
        )
      })}
    </Layout>
  )
}

export const query = graphql`
  query ($username: String!) {
    serverQuery {
      allUsers (username: $username) {
        firstName
        lastName
        username
        blogpostSet {
          edges {
            node {
              id
              title
              published
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
  }
`