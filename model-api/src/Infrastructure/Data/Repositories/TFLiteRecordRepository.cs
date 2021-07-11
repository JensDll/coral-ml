using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Dapper;
using Contracts;
using System.Data;
using System.IO;
using Application.Data;
using Application.Data.Repositories;
using Application.Data.Models;
using Contracts.Request;
using System.Text.Json;
using Contracts.Response;
using Domain.ValueObjects;
using Domain.Entities;
using Domain.DataTransfer;

namespace Infrastructure.Data.Repositories
{
    internal class TFLiteRecordRepository : ITFLiteRecordRepository
    {
        private readonly IConnectionFactory _connectionFactory;

        public TFLiteRecordRepository(IConnectionFactory connectionFactory)
        {
            _connectionFactory = connectionFactory;
        }

        public async Task<EnumerableEnvelope<TFLiteRecordModel>> GetAllAsync(Pagination pagination)
        {
            using var connection = _connectionFactory.NewConnection;

            (int skip, int take) = pagination.GetSkipTake();

            var parameter = new DynamicParameters();
            parameter.Add("skip", skip);
            parameter.Add("take", take);
            parameter.Add("total", dbType: DbType.Int32, direction: ParameterDirection.Output);

            var result = await connection.QueryAsync<string>(StoredProcedures.TFLiteRecord.GetAll,
                param: parameter,
                commandType: CommandType.StoredProcedure);

            int total = parameter.Get<int>("total");

            if (!result.Any())
            {
                return new EnumerableEnvelope<TFLiteRecordModel>
                {
                    Data = Enumerable.Empty<TFLiteRecordModel>(),
                    PageNumber = pagination.PageNumber,
                    PageSize = pagination.PageSize,
                    Total = total
                };
            }

            var models = JsonSerializer.Deserialize<IEnumerable<TFLiteRecordModel>>(string.Join("", result),
                new(JsonSerializerDefaults.Web));

            return new EnumerableEnvelope<TFLiteRecordModel>
            {
                Data = models,
                PageNumber = pagination.PageNumber,
                PageSize = pagination.PageSize,
                Total = total
            };
        }

        public async Task<byte[]> GetByIdAsync(int id)
        {
            using var connection = _connectionFactory.NewConnection;

            var zipContent = await connection.QuerySingleOrDefaultAsync<byte[]>(StoredProcedures.TFLiteRecord.GetById,
                param: new { id },
                commandType: CommandType.StoredProcedure);
            
            return zipContent;
        }

        public async Task<int> CreateAsync(string modelName, FormFileZipper zipper)
        {
            using var connection = _connectionFactory.NewConnection;

            byte[] zipContent = await zipper.CreateZipAsync();

            return await connection.QuerySingleAsync<int>(StoredProcedures.TFLiteRecord.Create,
                param: new { modelName, zipContent },
                commandType: CommandType.StoredProcedure);
        }

        public async Task<int> DeleteAsync(int id)
        {
            using var connection = _connectionFactory.NewConnection;

            return await connection.ExecuteAsync(StoredProcedures.TFLiteRecord.Delete,
                param: new { id },
                commandType: CommandType.StoredProcedure);
        }
    }
}
