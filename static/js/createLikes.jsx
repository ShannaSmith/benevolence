// alert('createLikes is :-)')
function CreateLike(props){
    const [like, setLikeText] = React.useState("");
    // const [user_answer, setUserAnswer] = React.useState("");
console.log('print out of props.prompt>>>>>>>>>>', props.prompt)
    function handleSubmit(evt){
        console.log('New like>>>>>>>>>>', like);
        console.log('prompt_id>>>>>>>>>>>', prompt_id);
        const data = {
            promptId:props.prompt.prompt_id,
            userAnswer:user_answer,
            like:like
        };
        fetch(`/likes/new/${props.recipient_id}`, {
            method:"POST",
            header: {
                "content-Type": 'application/json'
            },
            body:JSON.stringify(data)
        })
        .then(result => result.json())
        .then(result =>{
            console.log(`Ajax call for create event returned this: ${result}`)
            window.location.reload()
        })
    }
    return(
    <>
    
    <div>       
        <label htmlFor="prompt_reply" class="likes">{props.prompt.prompt_name}</label>
        <input type="text" name="prompt_reply" value={like} onChange={(evt) =>{setLikeText(evt.target.value)}} />
        <input type="hidden" name="prompt_id" value={props.prompt.prompt_id} />    
        <input type="submit" value="Submit" onClick={handleSubmit}/>
    </div>
    </>
    );   
}