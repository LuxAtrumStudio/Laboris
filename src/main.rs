#[macro_use]
extern crate diesel;
extern crate dotenv;
extern crate uuid;

use diesel::prelude::*;
use diesel::pg::PgConnection;
use dotenv::dotenv;
use std::env;

mod schema;
mod models;

use models::*;
use diesel::prelude::*;

pub fn establish_connection() -> PgConnection {
    dotenv().ok();

    let database_url = env::var("DATABASE_URL")
        .expect("DATABASE_URL must be set");
    PgConnection::establish(&database_url)
        .expect(&format!("Error connecting to {}", database_url))
}

pub fn main() {
    use schema::users::dsl::*;

    let connection = establish_connection();
    let results = users.limit(5).load::<User>(&connection).unwrap();
    println!("USERS: {}", results.len());
}
