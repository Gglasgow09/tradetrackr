import React, { useState } from 'react';

function SiteForm() {
    const [url, setUrl] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        // Add your logic here to handle the form submission
        // For example, you can make an API call to store the website in the backend
        console.log('Submitted URL:', url);
        setUrl(''); // Clear the input field after submission
    };

    const handleChange = (event) => {
        setUrl(event.target.value);
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Website URL:
                <input type="text" value={url} onChange={handleChange} />
            </label>
            <button type="submit">Add Website</button>
        </form>
    );
}

export default SiteForm;
