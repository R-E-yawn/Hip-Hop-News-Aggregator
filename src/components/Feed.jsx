import articles from '/Users/aryantyagi/rap-news/src/data.js'; 
import Card from './Card.jsx';

export default function Feed() {
  return (
    <div className="feed">
      {articles.map((data, key) => (
        <div key={key}>
          <Card articleData={data} />
        </div>
      ))}
    </div>
  );
}
