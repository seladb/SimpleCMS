import React from "react"

import { Link } from "gatsby"
import { FaThumbsUp, FaComment } from 'react-icons/fa';
import Layout from "../components/layout"
import formatDate from "../utils/utils"

const commentStyle = {
  border: '2px solid gray'
};

const commentHeaderStyle = {
  fontSize: '0.8em',
  fontStyle: 'italic'
}

export default ({data}) => {
  var node = data.serverQuery.allBlogPosts.edges[0].node
  return (
    <Layout>
      <h1>{node.title}</h1>
      <div>By <Link to={`/${node.writer.username}`}>@{node.writer.username}</Link></div>
      <div>Published: {formatDate(node.published)}</div>
      <div><FaThumbsUp /> {node.likeSet.length}</div>
      <p></p>
      <div>{node.content}</div>
      <p></p>
      <div><FaComment /> {node.commentSet.length}</div>
      {node.commentSet.map(comment => {
        return (
          <p style={commentStyle}>
            <div style={commentHeaderStyle}><Link to={`/${comment.addedBy.username}`}>@{comment.addedBy.username}</Link></div>
            <div style={commentHeaderStyle}>{formatDate(comment.added)}</div>
            <div>{comment.text}</div>
          </p>
          
        )
      })}
    </Layout>
  )
}

export const query = graphql`
  query ($id: ID!) {
    serverQuery {
      allBlogPosts (id: $id) {
        edges {
          node {
            title
            content
            published
            writer {
              username
            }
            likeSet {
              id
            }
            commentSet {
              text
              added
              addedBy {
                username
              }
            }
          }
        }
      }
    }
  }
`