using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace BD_1
{
    public partial class login : Form
    {
        public login()
        {
            InitializeComponent();
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void groupBox1_Enter(object sender, EventArgs e)
        {

        }
        private void login_Click(object sender, EventArgs e)
        {
            if(!this.loginBox.Text.Equals("") && !this.passBox.Text.Equals(""))
            {
                this.resp.Text = client.Login(this.loginBox.Text, this.passBox.Text);
                if( this.resp.Text== "Logged In")
                {
                    User user = new User(this.loginBox.Text, this.passBox.Text);
                    this.Hide();
                    user.Show();

                }
              
            }
            else
            {
                this.resp.Text = "Invalid Credentials";
            }
            
        }
    }
}
