using Application.Data;
using Application.Data.DataTransfer;
using Application.Data.DataTransfer.RecordType;
using Application.Data.Repositories;
using Contracts;
using Dapper;
using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace Infrastructure.Data.Repositories
{
    internal class RecordTypeRepository : IRecordTypeRepository
    {
        private readonly IConnectionFactory _connectionFactory;

        public RecordTypeRepository(IConnectionFactory connectionFactory)
        {
            _connectionFactory = connectionFactory;
        }

        public async Task<EnumerableEnevelope<RecordTypeGetAll>> GetAllAsync()
        {
            using var connection = _connectionFactory.NewConnection;

            var result = await connection.QueryAsync<RecordTypeGetAll>(StoredProcedures.RecordType.GetAll,
                commandType: CommandType.StoredProcedure);

            return new EnumerableEnevelope<RecordTypeGetAll>
            {
                Data = result
            };
        }
    }
}
