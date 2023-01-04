alert('createLikes is :-)')
function CreateLike(props){
    const [like, setLikeText] = React.useState("");
    const [prompt_id, setPromptID] = React.useState("");
    const [user_answer, setUserAnswer] = React.useState("");

    function handleSubmit(evt){
        console.log('New like>>>>>>>>>>', like);
        console.log('prompt_id>>>>>>>>>>>', prompt_id);
        const data = {
            promptId:prompt_id,
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
    for 
    </> 
    );   
}