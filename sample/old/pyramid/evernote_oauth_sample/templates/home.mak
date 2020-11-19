<%inherit file="base.mak"/>

<%block name="content">
  <p>
  <a href="${request.route_url('evernote_auth')}">Click here</a> to authorize this application to access your Evernote account. You will be directed to evernote.com to authorize access, then returned to this application after authorization is complete.
  </p>
</%block>

