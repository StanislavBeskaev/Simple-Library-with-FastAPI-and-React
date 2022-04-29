import React from "react"
import {setIssueYearGT, setIssueYearLT} from "../../store/actions/searchBooks"
import {connect} from "react-redux"
import {Input} from "antd"


const YearSearchGroup = (props) => (
  <div className="d-flex mb-3">
    <Input
      allowClear
      min={1}
      addonBefore="Год выпуска"
      className="number-input year-group"
      type="number"
      placeholder="от"
      value={props.issueYearGT}
      onChange={e => props.setIssueYearGT(e.target.value)}
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
      value={props.issueYearLT}
      onChange={e => props.setIssueYearLT(e.target.value)}
    />
  </div>
)

function mapStateToProps(state) {
  return {
    issueYearGT: state.searchBooks.params.issueYearGT,
    issueYearLT: state.searchBooks.params.issueYearLT,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    setIssueYearGT: number => dispatch(setIssueYearGT(number)),
    setIssueYearLT: number => dispatch(setIssueYearLT(number)),
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(YearSearchGroup)