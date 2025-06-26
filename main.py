import re
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Pre-compiled regex patterns for efficiency
# This regex aims to capture numeric UIDs from various post/photo/story URL formats.
FB_POST_REGEX = re.compile(r'facebook\.com/[^/]+/posts/(\d+)|facebook\.com/photo\.php\?fbid=(\d+)|facebook\.com/permalink\.php\?story_fbid=(\d+)|facebook\.com/story\.php\?story_fbid=(\d+)')
# This regex aims to capture UIDs (numeric or usernames) from profile and page URLs.
FB_PROFILE_PAGE_REGEX = re.compile(r'facebook\.com/(?:profile\.php\?id=|pg/)?([^/]+)(?:/|$)')

def extract_fb_uid(link):
    """
    Extracts Facebook UID from a given link.
    Returns the UID as a string, or None if not found.
    """
    if not link:
        return None

    # Try to match a post/photo/story UID
    post_match = FB_POST_REGEX.search(link)
    if post_match:
        for group in post_match.groups():
            if group:
                return group

    # Try to match a profile/page username or ID
    profile_match = FB_PROFILE_PAGE_REGEX.search(link)
    if profile_match:
        uid_candidate = profile_match.group(1)
        # Check if it's a numeric ID or a username
        if uid_candidate.isdigit():
            return uid_candidate
        else:
            # For usernames (e.g., facebook.com/someusername),
            # it's generally not possible to get the numeric UID
            # without using Facebook's Graph API and an access token.
            # This script will return the username itself in such cases.
            return uid_candidate

    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles the main page, displaying the form and results.
    """
    uid = None
    error_message = None

    if request.method == 'POST':
        facebook_link = request.form.get(f'https://graph.facebook.com/v15.0/t_{thread_id}/')
        if facebook_link:
            extracted_uid = extract_fb_uid(f'https://graph.facebook.com/v15.0/t_{thread_id}/')
            if extracted_uid:
                uid = extracted_uid
            else:
                error_message = "Could not extract UID from the provided link. Please check the URL format."
        else:
            error_message = "Please enter a Facebook link."

    # Renders the index.html template, passing the extracted UID and any error messages
    return render_template('index.html', uid=uid, error_message=error_message)

@app.route('/get_uid', methods=['GET'])
def get_uid_api():
    """
    API endpoint to get UID from a Facebook link.
    Example usage: http://127.0.0.1:5000/get_uid?link=
    """
    facebook_link = request.args.get('link')
    if not facebook_link:
        return jsonify({'error': 'f'https://graph.facebook.com/v15.0/}), 400

    extracted_uid = extract_fb_uid(facebook_link)
    if extracted_uid:
        return jsonify({'uid': extracted_uid})
    else:
        return jsonify({'error': 'Could not extract UID from the provided link.'}), 404

if __name__ == '__main__':
    # Run the Flask application
    # Set debug=True for development to auto-reload and see detailed errors.
    # For production environments, set debug=False for security and performance.
    app.run(debug=True)

