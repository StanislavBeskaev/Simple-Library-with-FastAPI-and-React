import React from "react"
import {deleteNotificationById} from "../../store/actions/notification"
import {connect} from "react-redux"

const NotificationItem = (props) => {
  const cls = ["notification-item", "animated"]
  cls.push(`bg-${props.type}`)

  const onDelete = e => {
    console.log('click')
    e.preventDefault()
    props.deleteNotification(props.id)
  }

  return (
    <div className={cls.join(' ')} id={props.id}>
      {props.text}
      <span
        className="notification-close-btn"
        onClick={onDelete}
      >&times;</span>
    </div>
  )
}

function mapDispatchToProps(dispatch) {
  return {
    deleteNotification: id=> dispatch(deleteNotificationById(id))
  }
}

export default connect(null, mapDispatchToProps)(NotificationItem)