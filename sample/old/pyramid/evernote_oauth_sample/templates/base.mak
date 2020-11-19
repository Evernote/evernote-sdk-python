<html>
  <head>
    <title>Evernote Python OAuth Demo</title>
  </head>
  <body>
    <h1>Evernote Python OAuth Demo</h1>

    <p>
      This application uses the <a href="http://docs.pylonsproject.org/en/latest/docs/pyramid.html">Pyramid framework</a> to demonstrate the use of OAuth to authenticate to the Evernote web service. OAuth support is implemented using the <a href="https://github.com/simplegeo/python-oauth2">oauth2</a>.
    </p>

    <p>
      On this page, we demonstrate how OAuth authentication might work in the real world.
      To see a step-by-step demonstration of how OAuth works, see <code>EDAMTest.py</code>.
    </p>

    <hr/>

    <h2>Evernote Authentication</h2>

    <%block name="content"></%block>

    <hr/>

    <p>
    <a href="${request.route_url('evernote_auth_reset')}">Click here</a> to start over
    </p>

  </body>
</html>

