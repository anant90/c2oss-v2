import React from 'react';
import TimeAgo from 'react-timeago';

import Issue from './Issue';
import Loader from '../Loader';

class IssuesUnit extends React.Component{
  constructor(){
    super();
    this.onFilterClick = this.onFilterClick.bind(this);
  }

  onFilterClick(ev){
    this.props.onFilterClick(ev.target.dataset.filter);
  }

  render(){
    let filterNodes = this.props.filters.map((filter, index) => {
      let isFilterActive = this.props.activeFilters.indexOf(filter) > -1;
      return (
        <span
          className={isFilterActive ? "filter active": "filter"}
          onClick={this.onFilterClick}
          data-filter={filter}
          key={index}>
          {filter}
        </span>
      );
    });
    let issueNodes = this.props.issues["issues"].map((issue, index) => {
      return <Issue key={index} index={index+1} {...issue} />
    });
    return (
      <div className="issues-unit">
        <div className="filters">
          {filterNodes}
        </div>

        <div className="sync-button-container">
            <button className={this.props.shouldShowSyncButton ? "sync-button": "sync-button disabled"}
              onClick={this.props.shouldShowSyncButton ? this.props.onSyncButtonClick: null}>
              {this.props.isSyncing ? <Loader color="white" />: "Sync with Github"}
            </button>
          {this.props.isSyncing ?
            <div className="last-synced">
              We will refresh the page after 5 minutes
            </div>
          : null}
          {!this.props.isSyncing && this.props.issues["last_synced"] ?
            <div className="last-synced">
              Last synced <TimeAgo date={this.props.issues["last_synced"]} />
            </div> : null}
        </div>

        {this.props.isFetchingIssues? <div className="loader-with-message"><Loader/><div className="message">Syncing with Github…</div></div> : null}
        {issueNodes}
      </div>
    )
  }
};

export default IssuesUnit;
