<%inherit file="base.mak"/>

<%block name="content">
<p style="color:green">
  Congratulations, you have successfully authorized this application to access your Evernote account!
</p>

<p>
  Your account contains the following notebooks:
</p>

<ul>
	% for notebook in notebooks:
    <li>${notebook.name}</li>
	% endfor
</ul>
</%block>
