function RecipientDetails(props) {
  return (
    <div id="log-out">
      <a href="/logout">Logout</a>
    </div>
  );
}
ReactDOM.render(<RecipientDetails/>, document.querySelector('#recipient-details'));