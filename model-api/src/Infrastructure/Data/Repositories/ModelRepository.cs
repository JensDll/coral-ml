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
using Domain.Entities;
using Application.Data;
using Application.Data.Repositories;
using Application.Data.Models;
using Application.Data.Services;
using Contracts.Request;
using System.Text.Json;
using Contracts.Response;

namespace Infrastructure.Data.Repositories
{
    internal class ModelRepository : IModelRepository
    {
        private readonly IConnectionFactory _connectionFactory;
        private readonly IPaginationService _paginationService;

        public ModelRepository(IConnectionFactory connectionFactory, IPaginationService paginationService)
        {
            _connectionFactory = connectionFactory;
            _paginationService = paginationService;
        }

        public async Task<EnumerableEnvelopeDto<TFLiteModelGetAllDto>> GetAllAsync(PaginationRequestDto paginationRequest)
        {
            using var cnn = _connectionFactory.NewConnection;

            (int skip, int take) = _paginationService.SkipTake(paginationRequest);

            var parameter = new DynamicParameters();
            parameter.Add("skip", skip);
            parameter.Add("take", take);
            parameter.Add("total", dbType: DbType.Int32, direction: ParameterDirection.Output);

            var result = await cnn.QueryAsync<string>(StoredProcedures.Model.GetAll,
                param: parameter,
                commandType: CommandType.StoredProcedure);

            int total = parameter.Get<int>("total");

            if (!result.Any())
            {
                return new()
                {
                    Data = Enumerable.Empty<TFLiteModelGetAllDto>(),
                    PageNumber = paginationRequest.PageNumber,
                    PageSize = paginationRequest.PageSize,
                    Total = total
                };
            }

            var models = JsonSerializer.Deserialize<IEnumerable<TFLiteModelModel>>(string.Join("", result),
                new(JsonSerializerDefaults.Web));

            return new()
            {
                Data = models.Select(model => new TFLiteModelGetAllDto
                {
                    Id = model.Id,
                    ModelName = model.ModelName
                }),
                PageNumber = paginationRequest.PageNumber,
                PageSize = paginationRequest.PageSize,
                Total = total
            };
        }

        public async Task<byte[]> GetByIdAsync(int id)
        {
            using var cnn = _connectionFactory.NewConnection;

            var model = await cnn.QuerySingleOrDefaultAsync<byte[]>(StoredProcedures.Model.GetById,
                param: new { id },
                commandType: CommandType.StoredProcedure);

            return model;
        }

        public async Task<int> CreateAsync(IFormFile modelFile)
        {
            using var cnn = _connectionFactory.NewConnection;
            using var memoryStream = new MemoryStream();

            await modelFile.CopyToAsync(memoryStream);

            return await cnn.QuerySingleAsync<int>(StoredProcedures.Model.Create,
                param: new { modelName = modelFile.FileName, model = memoryStream.ToArray() },
                commandType: CommandType.StoredProcedure);
        }

        public async Task<int> DeleteAsync(int id)
        {
            using var cnn = _connectionFactory.NewConnection;

            return await cnn.ExecuteAsync(StoredProcedures.Model.Delete,
                param: new { id },
                commandType: CommandType.StoredProcedure);
        }
    }
}
