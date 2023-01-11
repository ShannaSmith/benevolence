// alert('createLikes is :-)')
function CreateLike(props){
    console.log('print props>>>>>>', props);
    const [like, setLikeText] = React.useState("");
    const [user_answer, setUserAnswer] = React.useState("");
console.log('print out of props.prompt>>>>>>>>>>', props.prompt)

    function handleSubmit(evt){
        console.log('New like>>>>>>>>>>', like);
        console.log('prompt_id>>>>>>>>>>>', props.prompt.prompt_id);
        const data = {
             prompt_id:props.prompt.prompt_id,
             user_answer:user_answer,
            like:like,
            recipient_id:props.recipient_id
        };
        console.log('print recipient>>>>>>>>>>', props.recipient_id)
        fetch(`/likes/new/${props.recipient_id}`, {
            method:"POST",
            headers: {
                "Content-Type": 'application/json'
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
          
        <label htmlFor="prompt_reply" className="likes">{props.prompt.prompt_name}</label>
        <input type="text" name="prompt_reply" value={user_answer} onChange={(evt) =>{setUserAnswer(evt.target.value)}} />
        <input type="hidden" name="prompt_id" value={props.prompt.prompt_id} />    
        <input type="submit" value="Add interest" onClick={handleSubmit}/>
    </div>
    </>
    );   
}