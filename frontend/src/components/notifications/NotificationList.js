import React from "react"
import NotificationItem from "./NotificationItem"
import {connect} from "react-redux"


const NotificationList = (props) => {
  if (props.notifications.length === 0) return null

  const renderNotifications = () => {
    return props.notifications.map((notification, index) => {
      return <NotificationItem
                text={notification.text}
                type={notification.type}
                id={notification.id}
                key={notification.id}
              />
    })
  }

  return (
    <>
      <div className="notification-list">
        {renderNotifications()}
      </div>
    </>
  )
}

function mapStateToProps(state) {
  return {
    notifications: state.notifications.notifications
  }
}

export default connect(mapStateToProps)(NotificationList)
