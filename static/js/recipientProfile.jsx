function RecipientDetails(props) {
  return (
    <div id="log-out">
      <a href="/logout">Logout</a>
    </div>
  );
}
fetch(`/api/recipients_profile/${recipientId}`)
.then(response => response.json())
.then(responseJson =>{
    console.log(responseJson);
    ReactDOM.render(
        <RecipientDetails 
            recipientId={recipientId}
        />, 
        document.querySelector('#recipient-details')
    );
});

