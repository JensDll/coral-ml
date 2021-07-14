﻿using Microsoft.AspNetCore.Http;
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
using Contracts.Request;
using System.Text.Json;
using Domain.ValueObjects;
using Domain.Entities;
using Application.Data.DataTransfer;
using Application.Data.DataTransfer.Record;

namespace Infrastructure.Data.Repositories
{
    internal class RecordRepository : IRecordRepository
    {
        private readonly IConnectionFactory _connectionFactory;

        public RecordRepository(IConnectionFactory connectionFactory)
        {
            _connectionFactory = connectionFactory;
        }

        public async Task<PaginationEnvelope<RecordGetAll>>
            GetWithRecordTypeIdAsync(Pagination pagination, int recordTypeId)
        {
            using var connection = _connectionFactory.NewConnection;

            (int skip, int take) = pagination.GetSkipTake();

            var parameter = new DynamicParameters();
            parameter.Add(nameof(skip), skip);
            parameter.Add(nameof(take), take);
            parameter.Add(nameof(recordTypeId), recordTypeId);
            parameter.Add("total", dbType: DbType.Int32, direction: ParameterDirection.Output);

            var result = await connection
                .QueryAsync<string>(StoredProcedures.Record.GetWithRecordTypeId,
                    param: parameter,
                    commandType: CommandType.StoredProcedure);

            int total = parameter.Get<int>("total");

            var records = JsonSerializer.Deserialize<IEnumerable<RecordGetAll>>(string.Join("", result),
                new(JsonSerializerDefaults.Web));

            return new PaginationEnvelope<RecordGetAll>
            {
                Data = records,
                PageNumber = pagination.PageNumber,
                PageSize = pagination.PageSize,
                Total = total
            };
        }

        public async Task<RecordGetLoaded> GetLoadedAsync()
        {
            using var connection = _connectionFactory.NewConnection;

            var result = await connection.QueryAsync<string>(StoredProcedures.Record.GetLoaded,
                commandType: CommandType.StoredProcedure);

            if (!result.Any())
            {
                return null;
            }

            
            var loadedRecord = JsonSerializer
                .Deserialize<RecordGetLoaded>(string.Join("", result),
                    new(JsonSerializerDefaults.Web));

            return loadedRecord;
        }

        public async Task<RecordGetById> GetByIdAsync(int id)
        {
            using var connection = _connectionFactory.NewConnection;

            var result = await connection.QueryAsync<string>(StoredProcedures.Record.GetById,
                param: new { id },
                commandType: CommandType.StoredProcedure);

            if (!result.Any())
            {
                return null;
            }

            var record = JsonSerializer.Deserialize<RecordGetById>(string.Join("", result),
                new(JsonSerializerDefaults.Web));

            return record;
        }

        public async Task<byte[]> DownloadAsync(int id)
        {
            using var connection = _connectionFactory.NewConnection;

            var zipContent = await connection.QuerySingleOrDefaultAsync<byte[]>(StoredProcedures.Record.Download,
                param: new { id },
                commandType: CommandType.StoredProcedure);

            return zipContent;
        }

        public async Task<int> CreateAsync(RecordCreate createData)
        {
            using var connection = _connectionFactory.NewConnection;

            var parameter = new DynamicParameters();
            parameter.Add("modeFilelName", createData.ModelFileName);
            parameter.Add("labelFileName", createData.LabelFileName);
            parameter.Add("zipContent", createData.ZipContent);
            parameter.Add("recordTypeId", createData.RecordTypeId);

            return await connection.QuerySingleAsync<int>(StoredProcedures.Record.Create,
                param: parameter,
                commandType: CommandType.StoredProcedure);
        }

        public async Task<int> SetLoadedAsync(int recordId)
        {
            using var connection = _connectionFactory.NewConnection;

            return await connection.ExecuteAsync(StoredProcedures.Record.SetLoaded,
                param: new { recordId },
                commandType: CommandType.StoredProcedure);
        }

        public async Task<int> DeleteAsync(int id)
        {
            using var connection = _connectionFactory.NewConnection;

            return await connection.ExecuteAsync(StoredProcedures.Record.Delete,
                param: new { id },
                commandType: CommandType.StoredProcedure);
        }
    }
}