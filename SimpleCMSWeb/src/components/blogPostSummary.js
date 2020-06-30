import React from "react"
import { FaThumbsUp, FaComment } from 'react-icons/fa';
import { Link } from "gatsby"
import formatDate from "../utils/utils"

const BlogPostSummary = ({data}) => {
  return (
    <p key={data.id}>
      <Link to={`/${atob(data.id).split(':').pop()}`}><h3>{data.title}</h3></Link>
      {data.writer !== undefined ?
      <div>By <Link to={data.writer.username}>@{data.writer.username}</Link></div>
      :
      <div></div>
      }
      <div>Published: {formatDate(data.published)}</div>
      <div><FaThumbsUp />{data.likeSet.length} <FaComment /> {data.commentSet.length}</div>
    </p>
  )
}

export default BlogPostSummary