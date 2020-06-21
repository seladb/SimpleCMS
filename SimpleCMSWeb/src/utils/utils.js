const formatDate = (dateAsString) => {
    return new Intl.DateTimeFormat("en-GB", {
      year: "numeric",
      month: "long",
      day: "2-digit"
    }).format(new Date(dateAsString))
  }

export default formatDate