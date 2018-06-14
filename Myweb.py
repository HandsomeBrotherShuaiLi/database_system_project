import web
import model
urls=(
    '/','Index',

)
app=web.application(urls,globals())
t_globals={
    'datestr':web.datestr,
    'cookie':web.cookies,
}
render=web.template.render('templates',globals=t_globals)
login=web.form.Form(
    web.form.Textbox('username'),
    web.form.Password("password"),
    web.form.Button("login")
)



