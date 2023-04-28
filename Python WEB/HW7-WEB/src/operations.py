from datetime import datetime

from sqlalchemy import inspect
from sqlalchemy.exc import NoResultFound
from prettytable import PrettyTable

from .db import session

class CRUD:
    def add(self, table):
        inst = inspect(table)
        attrs = [c_attr.key for c_attr in inst.mapper.column_attrs]
        record_values = {}
        for attr in attrs[1:]:
            record_value = input(f"{attr.capitalize()} (Enter to skip): ")
            record_values[attr] = record_value
        session.add(table(**record_values))
        session.commit()
        return '\033[32mThe record added successfully!\033[0m'

    def delete(self, table):
        id_ = input("Id: ")
        try:
            record = (
                session.query(table)
                .select_from(table)
                .filter(table.id == id_)
                .one()
            )
            session.delete(record)
            session.commit()
            return f"\033[32mRecord with id {id_} was deleted!\033[0m"
        except NoResultFound:
            return f"There is no record with id {id_}"

    def show(self, table):
        table_columns = table.__table__.columns
        records = session.query(*table_columns).select_from(table).all()
        inst = inspect(table)
        attrs = [c_attr.key for c_attr in inst.mapper.column_attrs]
        pretty_table = PrettyTable(attrs)
        for record in records:
            pretty_table.add_row(record)
        return pretty_table

    def update(self, table):
        id_ = input("Id: ")
        table_columns = table.__table__.columns
        inst = inspect(table)
        attrs = [c_attr.key for c_attr in inst.mapper.column_attrs]
        query_record = session.query(*table_columns).filter(table.id == id_)
        record = query_record.one()
        if record:
            pretty_table = PrettyTable(attrs)
            pretty_table.add_row(record)
            print(pretty_table)
            record_values = {attr: value for attr, value in zip(attrs, record)}
            for attr in attrs[1:]:
                new_value = input(f"{attr.capitalize()} (Enter to skip): ")
                if new_value:
                    record_values[attr] = new_value
            if "date" in record_values:
                record_values["date"] = datetime.today().strftime("%Y-%m-%d")
            session.query(table).filter(table.id == id_).update(record_values)
            session.commit()
        return '\033[32mThe record updated successfully!\033[0m'

