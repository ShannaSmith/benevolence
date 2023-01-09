// alert('updateNote is connected :-)')

function UpdateNote(props){
    const [noteText , setNoteText] = React.useState(props.note.content)
    const [showForm, setShowForm] = React.useState(false);
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
            props.handleUpdateNote(noteText)
            setShowForm(false)
        })
    }
    function handleShowForm(evt){
       setShowForm(true);
    }
    return(
    <>
        <input type="submit" onClick={handleShowForm} value="update plan" />
        { 
        showForm && <div>
        <h1>update note</h1>
        <label htmlFor="note">Update Your plan here</label>
        <input type="textarea"  name="note" value={noteText} onChange={(evt) =>{setNoteText(evt.target.value)}} />
        <br/>
        <br/>
        <input type="submit" onClick={handleSubmit} value="Submit"/>
        </div> }
        
        </>
    );
}