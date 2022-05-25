terraform {
  required_providers {
    heroku = {
      source = "heroku/heroku"
    }
  }
}

provider "heroku" {
  email = ""
  api_key = ""
}

resource "heroku_app" "default" {
  name   = "csaba-netlogix-order-manager"
  region = "us"

  config_vars = {
    USERNAME = "netlogix"
    PASSWORD = "let_me_in"
  }
}

resource "heroku_build" "default" {
  app_id = heroku_app.default.id

  source {
    path = "./app"
  }
}

resource "heroku_addon" "database" {
  app_id = heroku_app.default.id
  plan   = "heroku-postgresql:hobby-dev"
}
