using Application.Data.Models;
using Application.Mapping.Model;
using Contracts.Response;
using Domain.DataTransfer;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Infrastructure.Mapping.Model
{
    internal class TFLiteRecordResponseMapper : ITFLiteRecordResponseMapper
    {
        public EnumerableEnvelope<TFLiteRecordGetAllDto>
            MapGetAllResponse(EnumerableEnvelope<TFLiteRecordModel> envelope)
        {
            return new EnumerableEnvelope<TFLiteRecordGetAllDto>
            {
                Data = envelope.Data.Select(model => new TFLiteRecordGetAllDto
                {
                    Id = model.Id,
                    ModelName = model.ModelName
                }),
                PageNumber = envelope.PageNumber,
                PageSize = envelope.PageSize,
                Total = envelope.Total
            };
        }
    }
}
