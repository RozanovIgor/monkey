# monkey

### Создание таблиц

```sql

create table coins(
    id varchar not null primary key,
    symbol varchar ,
    name varchar not null,
    img_url varchar not null
);

create table market_data(
    id serial primary key,
    coin_id varchar not null,
    current_price float not null,
    rank int not null,
    last_updated timestamp not null,

    constraint unique_price unique(coin_id, current_price, last_updated),
    foreign key (coin_id) references coins(id)
);


create table users(
    id serial not null primary key ,
    username varchar not null,
    password varchar not null,
    create_dt timestamp default current_timestamp,
    constraint unique_users unique(username, password)
);

create table users_portfolio_details(
    id serial not null primary key ,
    user_id int not null,
    market_data_id int not null,
    part_percent float not null,
    create_dt timestamp not null default current_timestamp,
    update_dt timestamp not null default current_timestamp,
    foreign key (user_id) references users(id),
    foreign key (market_data_id) references market_data(id)
);



-- Схема полностью соответствует users_portfolio_details, т.к логика в том, что портфель обезьяны тоже привязан к конкретному человеку, просто здесь будут другие market_data_id и part_percent
create table monkeys_portfolio_details(
    id serial not null primary key ,
    user_id int not null,
    market_data_id int not null,
    part_percent float not null,
    create_dt timestamp not null default current_timestamp,
    update_dt timestamp not null default current_timestamp,
    foreign key (user_id) references users(id),
    foreign key (market_data_id) references market_data(id)
);


create table user_portfolio(
    user_id int not null ,
    user_portfolio_id int not null,
    monkey_portfolio_id int not null,

    foreign key (user_id) references users(id),
    foreign key (user_portfolio_id) references users_portfolio_details(id),
    foreign key (monkey_portfolio_id) references monkeys_portfolio_details(id)
);

```