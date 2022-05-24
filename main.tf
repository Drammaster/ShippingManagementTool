terraform {
  required_providers {
    heroku = {
      source = "heroku/heroku"
    }
  }
}

provider "heroku" {
  email = "Csabi1996@windowslive.com"
  api_key = "a0e43661-7c68-4924-8f9f-611fc6ce7ff7"
}

resource "heroku_app" "netlogix" {
  name   = "dram-order-manager"
  region = "us"

  config_vars = {
    USERNAME = "netlogix"
    PASSWORD = "let_me_in"
  }
}

resource "heroku_build" "netlogix" {
  app_id = heroku_app.netlogix.id

  source {
    path = "./app"
  }
}

# resource "heroku_formation" "netlogix" {
#   app_id     = heroku_app.netlogix.id
#   type       = "web"
#   quantity   = 1
#   size       = "dev"
# }

resource "heroku_addon" "database" {
  app_id = heroku_app.netlogix.id
  plan   = "heroku-postgresql:hobby-dev"
}
