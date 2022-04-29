import React from "react"
import ReactDOM from "react-dom"
import {connect} from "react-redux"
import {hideDeleteConfirmModal} from "../../store/actions/deleteConfirm"


const DeleteConfirmModal = (props) => {

  const layoutClasses = ["delete-confirm-layout"]
  const modalClasses = ["card", "delete-confirm-modal"]

  if (props.visible) {
    layoutClasses.push("active")
    modalClasses.push("active")
  }

  const onDeleteClick = () => {
    props.hide()
    props.onDelete()
  }

  return ReactDOM.createPortal(
    <>
      <div className={layoutClasses.join(' ')} onClick={props.hide} />
      <div className={modalClasses.join(' ')} >
        <h5 className="card-header text-white bg-primary">Подтвердите удаление</h5>
        <div className="card-body">
          <p className="card-text">{props.text}</p>
          <div className="mt-4 d-flex justify-content-center">
            <button className="btn btn-danger" onClick={onDeleteClick}>Удалить</button>
            <button className="btn btn-primary ms-3" onClick={props.hide}>Отмена</button>
          </div>
        </div>
      </div>
    </>,
    document.getElementById('delete-confirm')
  )
}


function mapStateToProps(state) {
  return {
    visible: state.deleteConfirm.visible,
    text: state.deleteConfirm.text
  }
}

function mapDispatchToProps(dispatch) {
  return {
    hide: () => dispatch(hideDeleteConfirmModal()),
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(DeleteConfirmModal)
