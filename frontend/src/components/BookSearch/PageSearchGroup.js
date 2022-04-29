import React from "react"
import {setPageCountGT, setPageCountLT} from "../../store/actions/searchBooks"
import {connect} from "react-redux"
import {Input} from "antd"


const PageSearchGroup = (props) => (
  <div className="d-flex mb-3">
    <Input
      allowClear
      min={1}
      addonBefore="Страниц"
      className="number-input page-group"
      type="number"
      placeholder="от"
      value={props.pageCountGT}
      onChange={e => props.setPageCountGT(e.target.value)}
    />
    <Input
      className="input-splitter"
      placeholder="-"
      disabled
    />
    <Input
      allowClear
      min={1}
      className="number-input"
      type="number"
      placeholder="до"
      value={props.pageCountLT}
      onChange={e => props.setPageCountLT(e.target.value)}
    />
  </div>
)

function mapStateToProps(state) {
  return {
    pageCountGT: state.searchBooks.params.pageCountGT,
    pageCountLT: state.searchBooks.params.pageCountLT,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    setPageCountGT: number => dispatch(setPageCountGT(number)),
    setPageCountLT: number => dispatch(setPageCountLT(number)),
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(PageSearchGroup)