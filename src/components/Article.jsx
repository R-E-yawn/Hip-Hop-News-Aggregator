import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';

export default function Article() {
    const { mdFile } = useParams();
    const [markdownContent, setMarkdownContent] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadMarkdown = async () => {
            try {
                setLoading(true);
                
                const response = await fetch(`/articles/${mdFile}.md`);
                
                if (!response.ok) {
                    throw new Error(`Failed to load article: ${mdFile}`);
                }
                
                const content = await response.text();
                setMarkdownContent(content);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        if (mdFile) {
            loadMarkdown();
        }
    }, [mdFile]);

    if (loading) {
        return <div>Loading article...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div className="article-container">
            <ReactMarkdown>{markdownContent}</ReactMarkdown>
        </div>
    );
}