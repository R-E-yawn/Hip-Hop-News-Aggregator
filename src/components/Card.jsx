import { useNavigate } from 'react-router-dom'; 

export default function Card({articleData}){     
    const {urlToImage, title, url, source, score, comments} = articleData;     
    const navigate = useNavigate();     
    
    return (         
        <button 
            onClick={() => window.open(url)} 
            className={`card ${!urlToImage ? 'card-no-image' : ''}`}
        >             
            {urlToImage && <img src={urlToImage} alt={title} />}
            
            <div className="card-content">
                <h4>{title}</h4>
                
                {/* Show Reddit-specific info for posts without images */}
                {!urlToImage && (
                    <div className="reddit-info">
                        <span className="reddit-source">{source.name}</span>
                        <div className="reddit-stats">
                            <span>⬆️ {score}</span>
                            <span>💬 {comments}</span>
                        </div>
                    </div>
                )}
            </div>
        </button>      
    ) 
}