import Markdown from "markdown-to-jsx";
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom"; // Missing import!

export default function LoadPage() { // Remove unused prop
    const [post, setPost] = useState('');
    const { articleName } = useParams();
    
    useEffect(() => {
        // Use articleName directly, don't double the path
        import(`../articles/${articleName}.md`)
            .then(res => {
                fetch(res.default)
                    .then(res => res.text())
                    .then(res => setPost(res))
            })
            .catch(err => console.log(err))
    }, [articleName]); // Add dependency array!
    
    return (
        <div>
            <Markdown>
                {post}
            </Markdown>
        </div>
    )
}