// alert('updateNote is connected :-)')
function UpdateNote(props){
    const [noteText , setNoteText] = React.useState(props.note.content)

    function handleSubmit(evt){
        const data = {
            note_id: props.note.note_id,
            update_content: noteText
        };
        fetch("/update_note", {
            method:"POST",
            headers: {
                "Content-Type": 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(result => result.json())
        .then(result =>{
            // console.log(result)
            window.location.href=`/recipients_profile/${props.recipientId}`
        })
    }

    return(
    <>
    
        <h1>update note</h1>
        <label htmlFor="note">Update Your plan here</label>
        <input type="textarea"  name="note" value={noteText} onChange={(evt) =>{setNoteText(evt.target.value)}} />
        <br/>
        <br/>
        <input type="submit" onClick={handleSubmit} value="Submit"/>
    </>
    );
}